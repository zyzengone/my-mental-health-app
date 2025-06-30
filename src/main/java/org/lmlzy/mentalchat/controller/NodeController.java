package org.lmlzy.mentalchat.controller;

import com.alibaba.fastjson2.JSONObject;
import org.lmlzy.mentalchat.pojo.Disease;
import org.lmlzy.mentalchat.service.HealthService;
import org.neo4j.driver.types.Path;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/node")
public class NodeController {
    @Autowired
    public HealthService healthService;

    @RequestMapping("/getAll")
    public JSONObject getAll()
    {
        return healthService.getDiseaseByJsonFile();
    }
}
