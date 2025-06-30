package org.lmlzy.mentalchat.utils;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import jakarta.annotation.Resource;
import org.lmlzy.mentalchat.mapper.ConversationRecordMapper;
import org.lmlzy.mentalchat.pojo.ConversationRecord;
import org.lmlzy.mentalchat.pojo.SerializableMessage;
import org.springframework.ai.chat.messages.Message;
import org.springframework.ai.chat.messages.MessageType;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

@Component
public class MessageToRedisUtils {
    @Resource
    private RedisTemplate<String, List<Message>> redisTemplate;

    private final static String REDIS_KEY_PREFIX = "messages:";
    @Value("classpath:/rag/service.st")
    org.springframework.core.io.Resource systemPrompt;
    @Resource
    private ConversationRecordMapper conversationRecordMapper;

    private final static Integer MAX_SIZE = 10;
    public void saveSystemMessageToRedis(Message systemMessage, String sessionId) {
        List<Message> messages = redisTemplate.opsForValue().get(REDIS_KEY_PREFIX + sessionId);
        if (messages == null) {
            messages = new ArrayList<>();
        }
        if (messages.size() > MAX_SIZE) {
            messages = messages.subList(messages.size() - MAX_SIZE, messages.size());
        }
        // 确保SystemMessage始终在上下文中
        if (!messages.contains(systemMessage)) {
            messages.add(0, systemMessage); // 将SystemMessage放在最前面
        }
        redisTemplate.opsForValue().set(REDIS_KEY_PREFIX + sessionId, messages, 1, TimeUnit.HOURS); // 设置过期时间为1小时
    }

    public List<Message> getMessagesFromRedisOrDatabase(String sessionId) {
        List<Message> messages = redisTemplate.opsForValue().get(REDIS_KEY_PREFIX + sessionId);
        if (messages == null || messages.isEmpty()) {
            messages = fetchMessagesFromDatabase(sessionId);
            Message systemMessage = new SerializableMessage(String.valueOf(systemPrompt), MessageType.SYSTEM);
            if (!messages.contains(systemMessage)) {
                messages.add(0, systemMessage); // 将SystemMessage放在最前面
            }
            redisTemplate.opsForValue().set(REDIS_KEY_PREFIX + sessionId, messages, 1, TimeUnit.HOURS); // 设置过期时间为1小时
        }
        return messages;
    }

    public void saveMessageToRedis(Message message, String sessionId) {
        List<Message> messages = redisTemplate.opsForValue().get(REDIS_KEY_PREFIX + sessionId);
        if (messages == null) {
            messages = new ArrayList<>();
        }
        messages.add(message);
        if (messages.size() > MAX_SIZE) {
            messages = new ArrayList<>(messages.subList(messages.size() - MAX_SIZE, messages.size()));
        }
        redisTemplate.opsForValue().set(REDIS_KEY_PREFIX + sessionId, messages, 1, TimeUnit.HOURS); // 设置过期时间为1小时
    }

    private List<Message> fetchMessagesFromDatabase(String sessionId) {
        List<ConversationRecord> records = conversationRecordMapper.selectList(
                new QueryWrapper<ConversationRecord>()
                        .eq("session_id", sessionId)
                        .orderByAsc("timestamp")
                        .last("LIMIT " + MAX_SIZE)
        );

        List<Message> messages = new ArrayList<>();
        for (ConversationRecord record : records) {
            if (record.getUserFlag()) {
                messages.add(new SerializableMessage(record.getMessage(), MessageType.USER));
            } else {
                messages.add(new SerializableMessage(record.getMessage(), MessageType.ASSISTANT));
            }
        }
        return messages;
    }

}
