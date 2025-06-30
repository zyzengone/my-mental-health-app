package org.lmlzy.mentalchat;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("org.lmlzy.mentalchat.mapper")
public class MentalchatApplication {

    public static void main(String[] args) {
        SpringApplication.run(MentalchatApplication.class, args);
    }

}
