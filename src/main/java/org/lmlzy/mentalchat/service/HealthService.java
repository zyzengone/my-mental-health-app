package org.lmlzy.mentalchat.service;

import com.alibaba.fastjson2.JSON;
import com.alibaba.fastjson2.JSONObject;
import com.alibaba.fastjson2.util.IOUtils;
import org.lmlzy.mentalchat.pojo.Disease;
import org.lmlzy.mentalchat.pojo.PatientDescription;
import org.lmlzy.mentalchat.pojo.Symptom;
import org.lmlzy.mentalchat.repository.DescriptionRepository;
import org.lmlzy.mentalchat.repository.DiseaseRepository;
import org.lmlzy.mentalchat.repository.SymptomRepository;
import org.lmlzy.mentalchat.utils.Neo4jDataUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Service
public class HealthService {
    @Autowired
    private DiseaseRepository diseaseRepository;
    @Autowired
    private SymptomRepository symptomRepository;
    @Autowired
    private DescriptionRepository descriptionRepository;
    @Autowired
    private Neo4jDataUtils neo4jDataUtils;
    @Value("classpath:node.json")
    private Resource filePath;

    public void createRelationship() {
        List<Disease> diseases = new ArrayList<>();
        List<Symptom> symptoms = new ArrayList<>();
        List<PatientDescription> patientDescriptions = new ArrayList<>();
        neo4jDataUtils.getJsonData(diseases, symptoms, patientDescriptions);
        diseaseRepository.saveAll(diseases);
        symptomRepository.saveAll(symptoms);
        descriptionRepository.saveAll(patientDescriptions);
    }
    public JSONObject getAllDisease() {
        List<Disease> diseases = diseaseRepository.findAll();
        List<Symptom> symptoms = symptomRepository.findAll();
        List<JSONObject> diseaseRelationList = new ArrayList<>();
        List<JSONObject> nodeList = new ArrayList<>();
        List<JSONObject> diseaseList = new ArrayList<>();
        for (Symptom symptom : symptoms){
            for (PatientDescription description : symptom.getDescriptions()){
                JSONObject jsonObject = new JSONObject();
                jsonObject.put("source", "S"+symptom.getId());
                jsonObject.put("target", description.getId());
                jsonObject.put("relate", "description");
//                diseaseRelationList.add(jsonObject);
            }
            JSONObject jsonObject = new JSONObject();
            jsonObject.put("id", "S"+symptom.getId());
            jsonObject.put("name", symptom.getName());
            jsonObject.put("label", "symptom");
            nodeList.add(jsonObject);
        }
        for (Disease disease : diseases){
            for (Symptom symptom : disease.getCauses()){
                JSONObject jsonObject = new JSONObject();
                jsonObject.put("source", "D"+disease.getId());
                jsonObject.put("target", "S"+symptom.getId());
                jsonObject.put("relate", "cause");
                diseaseRelationList.add(jsonObject);
            }
            JSONObject jsonObject = new JSONObject();
            jsonObject.put("id", "D"+disease.getId());
            jsonObject.put("name", disease.getName());
            jsonObject.put("label", "disease");
            nodeList.add(jsonObject);
        }
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("nodes", nodeList);
        jsonObject.put("links", diseaseRelationList);
        return jsonObject;
    }
    public JSONObject getDiseaseByJsonFile() {
        try (InputStream inputStream = filePath.getInputStream()) {
            // 读取文件内容并解析为 JSONObject
            String content = new String(inputStream.readAllBytes());
            return JSON.parseObject(content);
        } catch (IOException e) {
            e.printStackTrace();
            throw new RuntimeException("Failed to read JSON file", e);
        }
    }

}
