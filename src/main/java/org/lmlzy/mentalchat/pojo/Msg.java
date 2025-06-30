package org.lmlzy.mentalchat.pojo;

import lombok.Data;

@Data
public class Msg {
    String message;
    Long userId;
    String sessionId;
    int userFlag;
}
