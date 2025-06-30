package org.lmlzy.mentalchat.service;

import org.lmlzy.mentalchat.mapper.SessionMapper;
import org.lmlzy.mentalchat.mapper.UserMapper;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.ollama.OllamaChatModel;
import org.springframework.ai.ollama.api.OllamaOptions;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

@Service
public class PersonalityService {
    @Autowired
    private OllamaChatModel chatModel;

    @Autowired
    private SessionMapper sessionMapper;

    @Autowired
    private UserMapper userMapper;
    public String analyzerPersonality(Long userId) {
        List<String> message =  sessionMapper.getUserSessionsChat(userId);
        String result = message.stream()
                .collect(Collectors.joining("||"));
        ChatResponse response = chatModel.call(
                new Prompt(
                        "根据以下文本给出分析这个人的MBTI人格（仅给出一个结果，不要包含其他文字）：" + result,
                        OllamaOptions.builder()
                                .model("qwen2.5:14b")
                                .temperature(0.4)
                                .build()
                ));
        String res = response.getResult().getOutput().getText();
// 优化后的正则表达式
        Pattern pattern = Pattern.compile(
                "\\b(INFJ|ENTP|INTP|INTJ|ENTJ|ENFJ|INFP|ENFP|ISFP|ISTP|ISFJ|ISTJ|ESTP|ESFP|ESTJ|ESFJ)\\b",
                Pattern.CASE_INSENSITIVE
        );
        Matcher matcher = pattern.matcher(res);
        String per = matcher.find() ? matcher.group() : "分析中";
        userMapper.updatePersonality(userId,per);
        return per;
    }
    public String getPersonality(Long userId) {
        String personality = userMapper.getPersonality(userId);
        return personality == null ? "" : personality;
    }
}
