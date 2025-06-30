package org.lmlzy.mentalchat.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class JwtConfig {

    @Bean
    public String jwtSecretKey() {
        return "your-very-secret-key"; // 替换为你的密钥
    }
}
