package org.lmlzy.mentalchat;

import org.junit.jupiter.api.Test;
import org.lmlzy.mentalchat.repository.DescriptionRepository;
import org.lmlzy.mentalchat.repository.DiseaseRepository;
import org.lmlzy.mentalchat.repository.SymptomRepository;
import org.lmlzy.mentalchat.service.HealthService;
import org.lmlzy.mentalchat.utils.Neo4jDataUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@SpringBootTest
class MentalchatApplicationTests {
    @Autowired
    Neo4jDataUtils neo4jDataUtils;
    @Autowired
    DiseaseRepository diseaseRepository;
    @Autowired
    SymptomRepository symptomRepository;
    @Autowired
    DescriptionRepository descriptionRepository;
    @Autowired
    HealthService healthService;
    @Test
    void test() {
//        diseaseRepository.deleteAll();
//        symptomRepository.deleteAll();
//        descriptionRepository.deleteAll();
//        healthService.createRelationship();

    }
    @Test
    public void groupAnagrams() {
        String[] strs = {"eat", "tea", "tan", "ate", "nat", "bat"};
        List<String> list = Arrays.asList(strs);
        List<List<String>> res = list.stream().collect(Collectors.groupingBy(s -> {
            char[] chars = s.toCharArray();
            Arrays.sort(chars);
            return new String(chars);
        })).values().stream().map(ArrayList::new).collect(Collectors.toList());
        System.out.println(res.get(0).get(0));
    }
    @Test
    void contextLoads() {
    }

}
