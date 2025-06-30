package org.lmlzy.mentalchat.pojo;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import java.util.HashSet;
import java.util.Set;

@TableName("role")
public class Role {
    @TableId(type = IdType.AUTO)
    private Long id;
    private String name; // 角色名称

    private Set<Permission> permissions = new HashSet<>();

    // Getters and Setters
}
