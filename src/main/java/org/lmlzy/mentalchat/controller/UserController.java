package org.lmlzy.mentalchat.controller;

import com.alibaba.fastjson2.JSONObject;
import jakarta.annotation.Resource;
import org.lmlzy.mentalchat.pojo.User;
import org.lmlzy.mentalchat.pojo.UserToken;
import org.lmlzy.mentalchat.service.UserService;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/user")
public class UserController {
    @Resource
    UserService userService;

    @RequestMapping("/login")
    public JSONObject login(@RequestBody User user){
        User id = userService.selectUserByUsername(user.getUsername(),user.getPassword());
        JSONObject data = new JSONObject();
        if (id == null){

            data.put("data","-1");
            return data;
        }
        UserToken userToken = new UserToken(userService.generateToken(id.getId()),id.getId());
        data.put("data",userToken);
        return data;
    }

}
