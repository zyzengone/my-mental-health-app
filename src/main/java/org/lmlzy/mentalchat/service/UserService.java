package org.lmlzy.mentalchat.service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import org.lmlzy.mentalchat.mapper.UserMapper;
import org.lmlzy.mentalchat.pojo.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;

@Service
public class UserService extends ServiceImpl<UserMapper, User> {

    @Autowired
    UserMapper userMapper;

    @Value("${jwt.secret.key}")
    private String secretKey;

    public User selectUserByUsername(String name, String password) {
        return userMapper.selectUserByUsername(name, password);
    }

    public List<String> getUserPermissions(Long userId) {
        return userMapper.getUserPermissions(userId);
    }

    public String getUserIdFromToken(String token) {
        try {
            return Jwts.parserBuilder()
                    .setSigningKey(secretKey)
                    .build()
                    .parseClaimsJws(token)
                    .getBody()
                    .getSubject();
        } catch (ExpiredJwtException e) {
            // 处理Token过期的情况
            throw new RuntimeException("Token已过期", e);
        } catch (Exception e) {
            // 处理其他异常情况
            throw new RuntimeException("无效的Token", e);
        }
    }


    public String generateToken(Long userId) {
        // 设置过期时间，例如1小时后过期
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + 3600000);
        return Jwts.builder()
                .setSubject(userId.toString())
                .setIssuedAt(now)
                .setExpiration(expiryDate)
                .signWith(SignatureAlgorithm.HS512, secretKey)
                .compact();
    }
}
