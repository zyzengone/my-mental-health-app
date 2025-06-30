package org.lmlzy.mentalchat.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.lmlzy.mentalchat.pojo.Session;
import org.lmlzy.mentalchat.pojo.UserWarning;

import java.util.List;

@Mapper
public interface SessionMapper extends BaseMapper<Session> {
    @Select("SELECT CONTENT FROM sessions left join SPRING_AI_CHAT_MEMORY on session_id = conversation_id " +
            "WHERE user_id = #{userId} and type='USER' order by timestamp limit 10")
    List<String> getUserSessionsChat(Long userId);

    @Insert("INSERT INTO user_warning(user_id,content,type) values(#{userId},#{reason},#{type})")
    void insertWarning(Long userId, String reason,String type);

    @Select("SELECT * FROM user_warning")
    List<UserWarning> getUserWarning();
}
