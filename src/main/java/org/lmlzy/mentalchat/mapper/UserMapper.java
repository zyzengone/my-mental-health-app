package org.lmlzy.mentalchat.mapper;


import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.lmlzy.mentalchat.pojo.User;

import java.util.List;

@Mapper
public interface UserMapper extends BaseMapper<User> {
    @Select("SELECT * FROM user WHERE name = #{username} and password= #{password}")
    User selectUserByUsername(String username,String password);

    @Select("SELECT p.name FROM user u " +
              "JOIN user_role ur ON u.id = ur.user_id " +
              "JOIN role r ON ur.role_id = r.id " +
              "JOIN role_permission rp ON r.id = rp.role_id " +
              "JOIN permission p ON rp.permission_id = p.id " +
              "WHERE u.id = #{userId}")
    List<String> getUserPermissions(@Param("userId") Long userId);

    @Select("SELECT user_id FROM user_token WHERE token = #{token}")
    Long getUserIdFromToken(String token);

    @Select("select personality from personality where user_id=#{userId}")
    String getPersonality(Long userId);

    @Insert("INSERT INTO personality (user_id, personality) VALUES (#{userId}, #{per}) " +
            "ON DUPLICATE KEY UPDATE personality = #{per}")
    void updatePersonality(Long userId, String per);
}

