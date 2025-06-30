package org.lmlzy.mentalchat.pojo;

import org.springframework.ai.chat.messages.Message;
import org.springframework.ai.chat.messages.MessageType;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.core.io.Resource;

import java.io.Serial;
import java.io.Serializable;
import java.util.List;
import java.util.Map;
import java.util.Objects;

public class SerializableMessage implements Serializable, Message {
    private String textContent;
    private MessageType messageType;

    public SerializableMessage(String textContent, MessageType messageType) {
        this.messageType = messageType;
        this.textContent = textContent;
    }

    @Override
    public MessageType getMessageType() {
        return  messageType;
    }

    @Override
    public String getText() {
        return textContent;
    }


    @Override
    public Map<String, Object> getMetadata() {
        return null;
    }


    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Message message = (SerializableMessage) obj;
        return Objects.equals(textContent, message.getText()) && messageType == message.getMessageType();
    }
}
