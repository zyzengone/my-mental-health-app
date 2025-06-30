package org.lmlzy.mentalchat.interceptor;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.lmlzy.mentalchat.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import java.util.List;

@Component
public class AuthorizationInterceptor implements HandlerInterceptor {
    @Autowired
    private UserService userService;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String token = request.getHeader("Authorization");
        Long userId = null;
        System.out.println(request.getRequestURI());
        System.out.println(request.getRequestURL());
        try {
            String userIdstr = userService.getUserIdFromToken(token);
            userId = Long.valueOf(userIdstr);
        } catch (Exception e){
            response.setStatus(HttpServletResponse.SC_FORBIDDEN);
            return false;
        }

        List<String> permissions = userService.getUserPermissions(userId);
        System.out.println(request.getRequestURI());
        // 根据请求路径判断所需的权限，并检查用户是否拥有这些权限
        if (!permissions.contains(request.getRequestURI())) {
            response.setStatus(HttpServletResponse.SC_OK);
            return false;
        }
        return true;
    }
}
