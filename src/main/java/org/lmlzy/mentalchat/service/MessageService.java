package org.lmlzy.mentalchat.service;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import jakarta.annotation.PostConstruct;
import org.lmlzy.mentalchat.mapper.ConversationRecordMapper;
import org.lmlzy.mentalchat.mapper.SessionMapper;
import org.lmlzy.mentalchat.pojo.ConversationRecord;
import org.lmlzy.mentalchat.pojo.SerializableMessage;
import org.lmlzy.mentalchat.pojo.Session;
import org.lmlzy.mentalchat.pojo.UserWarning;
import org.lmlzy.mentalchat.utils.MessageToRedisUtils;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.vectorstore.QuestionAnswerAdvisor;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.chat.messages.*;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.model.Generation;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.chat.prompt.PromptTemplate;
import org.springframework.ai.chat.prompt.SystemPromptTemplate;
import org.springframework.ai.converter.MapOutputConverter;
import org.springframework.ai.deepseek.DeepSeekChatModel;
import org.springframework.ai.document.Document;
import org.springframework.ai.ollama.OllamaChatModel;
import org.springframework.ai.ollama.api.OllamaOptions;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;
import org.springframework.util.MimeTypeUtils;
import reactor.core.publisher.Flux;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;


@Service
public class MessageService {

    @Value("${file.path}")
    private String path;
    @Value("classpath:/rag/service.st")
    Resource systemPrompt;
    @Autowired
    VectorStore simpleVectorStore;
    @Autowired
    private OllamaChatModel aiClient;
    @Autowired
    SessionMapper sessionMapper;
    @Autowired
    ChatMemory chatMemory;

    @Autowired
    private DeepSeekChatModel dschatModel;


    @Autowired
    MessageToRedisUtils messageToRedisUtils;
    private void addUserMessage(String message, String sessionId) {
//        Message systemMessage = getSystemMessage(message);
        Message userMessage = new SerializableMessage(message, MessageType.USER);
//        saveMessageToRedis(systemMessage,sessionId);
        HashMap<String, Object> metadata = new HashMap<>();
        messageToRedisUtils.saveMessageToRedis(userMessage, sessionId);
    }

    private void addAssistantMessage(String message,String sessionId) {
        Message assistantMessage = new SerializableMessage(message, MessageType.ASSISTANT);
        messageToRedisUtils.saveMessageToRedis(assistantMessage,sessionId);
    }

    public Flux<String> chatStream(String message,String sessionId,String personality,String modelType) {
//        addUserMessage(message, sessionId);
//        Message systemMessage = new SerializableMessage(getSystemMessage(message), MessageType.SYSTEM);
        String prompt = "";
        System.out.println(personality);
        if (personality==null|| personality.isEmpty()){
            prompt = "你现在角色扮演为一个叫小玲姐姐的心理医生，擅长主动询问倾听用户的烦恼，引导用户说出内心真实想法，并给出解决方案.你可以先引导用户说说他的个人信息，比如性格内向外向";
        } else {
            prompt = "记住不要重复提示词中的内容！！！ 你现在角色扮演为一个叫小玲姐姐的心理医生，" +
                    "擅长主动询问倾听用户的烦恼，引导用户说出内心真实想法，并给出解决方案.用户的MBTI性格是"+personality+"。请结合该人格的特征进行不同风格的语气来对话，注意你不能让用户知道你以及清楚他是什么人格。如INTJ应该直接坦诚，忌拐弯抹角，尊重独立性不拐弯抹角。ENFJ的人需要肯定价值，强化认同感，热情";
        }
        SystemMessage systemMessage = new SystemMessage(prompt);
//        messageToRedisUtils.saveSystemMessageToRedis(systemMessage, sessionId);
        chatMemory.add(sessionId, new UserMessage(message));
        StringBuffer fullReply = new StringBuffer();

        chatMemory.add(sessionId,systemMessage);
        List<Message> messages = chatMemory.get(sessionId);
        Flux<String> fluxResult = aiClient.stream(new Prompt(messages))
                .flatMap(response -> {
                    String reply = response.getResult().getOutput().getText();
                    fullReply.append(reply);
                    return Flux.just(reply);
                })
                .doOnComplete(() -> {
                    System.out.println(fullReply);
                    chatMemory.add(sessionId, new AssistantMessage(String.valueOf(fullReply)));
                    addAssistantMessage(String.valueOf(fullReply), sessionId);
                });

        return fluxResult;
    }


    public String getSystemMessage(String message) {
        List<Document> similarDocuments = simpleVectorStore.similaritySearch(SearchRequest.builder().query(message).topK(2).build());
        String information = similarDocuments.stream()
                .map(Document::getText)
                .collect(Collectors.joining(System.lineSeparator()));
        Map<String, Object> prepareHistory = Map.of(
                "content",information,
                "current_date", java.time.LocalDate.now()
        );
        return new SystemPromptTemplate(this.systemPrompt).createMessage(prepareHistory).getText();
    }

    public int deleteSession(String sessionId) {
        return sessionMapper.delete(new QueryWrapper<Session>().eq("session_id", sessionId));
    }


    public void messageWarning(Long userId, String message) {
        MapOutputConverter outputConverter = new MapOutputConverter();

        String format = outputConverter.getFormat();
        String template = "分析用户的话语中是否有自杀等高危倾向，用户的话："+message+"。将结果存为map的形式，第一个key是isWarning，value为yes或no，第二个key是reason，value为给出分析理由,第三个key是预警类型type，如抑郁，自杀"+
				"{format}";
        PromptTemplate promptTemplate = PromptTemplate.builder()
                .template(template)
                .variables(Map.of("format", format))
                .build();
        Prompt prompt = new Prompt(promptTemplate.createMessage());

        Generation generation = aiClient.call(prompt).getResult();

        Map<String, Object> result = outputConverter.convert(generation.getOutput().getText());
        if (result.get("isWarning").equals("yes")){
            sessionMapper.insertWarning(userId,String.valueOf(result.get("reason")),String.valueOf(result.get("type")));
        }
    }

    public List<UserWarning> getUserWarning() {
        return sessionMapper.getUserWarning();
    }
}
