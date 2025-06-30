package org.lmlzy.mentalchat.pojo;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@TableName("user_warning")
@Data
public class UserWarning {
    private Long userId;
    private String content;
    private String warningTime;
    private String isAck;
    private String type;

}
