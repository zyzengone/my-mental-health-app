package org.lmlzy.mentalchat.pojo;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import java.util.HashSet;
import java.util.Set;
@TableName("permission")
public class Permission {
    @TableId(type = IdType.AUTO)
    private Long id;
    private String name; // 权限名称

    private Set<Role> roles = new HashSet<>();

    // Getters and Setters
}
