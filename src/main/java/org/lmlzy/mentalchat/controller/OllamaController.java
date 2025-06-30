package org.lmlzy.mentalchat.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import org.lmlzy.mentalchat.pojo.*;
import org.lmlzy.mentalchat.service.MessageService;
import org.lmlzy.mentalchat.mapper.ConversationRecordMapper;
import org.lmlzy.mentalchat.mapper.SessionMapper;
import org.lmlzy.mentalchat.service.PersonalityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ResourceLoader;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import reactor.core.publisher.Flux;

import java.io.File;
import java.io.IOException;
import java.sql.Timestamp;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/ollama")
public class OllamaController {


    @Value("${file.path}")
    private String path;

    @Autowired
    private ConversationRecordMapper conversationRecordMapper;

    @Autowired
    private ResourceLoader resourceLoader;
    @Autowired
    private SessionMapper sessionMapper;
    @Autowired
    private MessageService messageService;

    @Autowired
    private PersonalityService personalityService;
    @PostMapping(value = "/chatStream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> chatStream(@RequestBody ConversationRecord msg) {
        String sessionId = msg.getSessionId();
        Long userId = msg.getUserId();
        String modelType = msg.getModelType();
        String personality = personalityService.getPersonality(userId);
        String message = msg.getMessage();
        messageService.messageWarning(userId,message);
        if (sessionId == null || sessionId.isEmpty()) {
            sessionId = createNewSession(userId).getSessionId();
        }
        saveConversationRecord(userId, sessionId, message, true);
        String finalSessionId = sessionId;

        StringBuffer fullReply = new StringBuffer();

        return messageService.chatStream(message, sessionId, personality,modelType)
                .doOnNext(fullReply::append) // 拼接响应内容
                .doOnComplete(() -> saveConversationRecord(userId, finalSessionId, fullReply.toString(), false)) // 流结束时保存完整记录
                .flatMapSequential(Flux::just);
    }

    /**
     * 处理图片消息
     */
//    @PostMapping("/chatImage")
//    public Flux<String> chatImage(@RequestBody ConversationRecord msg) {
//        String sessionId = msg.getSessionId();
//        Long userId = msg.getUserId();
//        String message = msg.getMessage();
//        String[] urls = message.split("/");
//        String fileName = urls[urls.length-1];
//        Resource resource = new FileSystemResource(path+"/"+fileName);
//        if (sessionId == null || sessionId.isEmpty()) {
//            sessionId = createNewSession(userId).getSessionId();
//        }
//        saveConversationRecord(userId, sessionId, message, true);
//        String finalSessionId = sessionId;
//
//        StringBuffer fullReply = new StringBuffer();
//
//        return messageService.chatStream(resource, sessionId)
//                .doOnNext(fullReply::append) // 拼接响应内容
//                .doOnComplete(() -> saveConversationRecord(userId, finalSessionId, fullReply.toString(), false)) // 流结束时保存完整记录
//                .flatMapSequential(Flux::just);
//
//    }

    @PostMapping("/uploadImage")
    public ApiResponse<String> uploadImage(
            @RequestPart("file") MultipartFile file,
            @RequestParam Long userId,
            @RequestParam String sessionId) {

        if (file.isEmpty()) {
            return ApiResponse.error(400, "上传的文件不能为空");
        }

        try {
            // 生成唯一的文件名
            String fileName = UUID.randomUUID().toString() + "_" + file.getOriginalFilename();
            File file1 = new File(path);
            if (!file1.exists()) {
                file1.mkdirs();
            }
            File dest = new File(path, fileName);
            file.transferTo(dest);
            // 保存图片记录到数据库
            saveConversationRecord(userId, sessionId, dest.getPath(), true);

            return ApiResponse.success(dest.getName());
        } catch (IOException e) {
            e.printStackTrace();
            return ApiResponse.error(500, "文件上传失败");
        }
    }

    /**
     * 创建新的会话
     */
    @PostMapping("/createSession")
    public ApiResponse<Session> createSession(@RequestParam Long userId) {
        return ApiResponse.success(createNewSession(userId));
    }

    /**
     * 删除会话
     */
    @PostMapping("/deleteSession")
    public ApiResponse<Integer> deleteSession(@RequestParam String sessionId) {
        int res = messageService.deleteSession(sessionId);
        if (res > 0){
            return ApiResponse.success(1);
        }
        return ApiResponse.error(400,"删除会话失败");
    }

    private Session createNewSession(Long userId) {
        Session session = new Session();
        session.setUserId(userId);
        session.setSessionId(UUID.randomUUID().toString());
        session.setCreatedAt(new Timestamp(System.currentTimeMillis()));
        sessionMapper.insert(session);
        saveConversationRecord(userId, session.getSessionId(),
                "你好，我是小玲姐姐，有什么事情都可以向我倾述", false);
        return session;
    }

    /**
     * 获取用户的会话列表
     */
    @GetMapping("/sessions")
    public ApiResponse<List<Session>> getUserSessions(@RequestParam Long userId) {
        List<Session> list = sessionMapper.selectList(new QueryWrapper<Session>().eq("user_id", userId));
        return ApiResponse.success(list);
    }

    /**
     * 获取特定会话的聊天历史记录
     */
    @GetMapping("/conversationHistory")
    public ApiResponse<List<ConversationRecord>> getConversationHistory(@RequestParam String sessionId) {
        List<ConversationRecord> list = conversationRecordMapper.selectList(new QueryWrapper<ConversationRecord>().eq("session_id", sessionId));
        return ApiResponse.success(list);
    }

    private void saveConversationRecord(Long userId, String sessionId, String message, boolean isUser) {
        ConversationRecord record = new ConversationRecord();
        record.setUserId(userId);
        record.setSessionId(sessionId);
        record.setMessage(message);
        record.setUserFlag(isUser);
        record.setTimestamp(new Timestamp(System.currentTimeMillis()));
        conversationRecordMapper.insert(record);
    }

    @GetMapping("/updatePersonality")
    public ApiResponse<String> updatePersonality(@RequestParam Long userId) {
        String personality = personalityService.analyzerPersonality(userId);
        return ApiResponse.success(personality);
    }

    @GetMapping("/getPersonality")
    public ApiResponse<String> getPersonality(@RequestParam Long userId) {
        String personality = personalityService.getPersonality(userId);
        return ApiResponse.success(personality);
    }

    @GetMapping("/getUserWarning")
    public ApiResponse<List<UserWarning>> getUserWarning() {
        return ApiResponse.success(messageService.getUserWarning());
    }
}
