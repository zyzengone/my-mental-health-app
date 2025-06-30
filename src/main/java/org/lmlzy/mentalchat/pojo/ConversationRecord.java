package org.lmlzy.mentalchat.pojo;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.sql.Timestamp;

@Data
@TableName("conversation_records")
public class ConversationRecord {
    private Long id;
    private Long userId;
    private String sessionId;
    private Timestamp timestamp;
    private String message;
    private String modelType;
    private Boolean userFlag;

    // Getters and Setters
}
