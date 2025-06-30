package org.lmlzy.mentalchat.utils;

import com.alibaba.fastjson2.JSON;
import com.alibaba.fastjson2.JSONArray;
import com.alibaba.fastjson2.JSONObject;
import org.lmlzy.mentalchat.pojo.Disease;
import org.lmlzy.mentalchat.pojo.PatientDescription;
import org.lmlzy.mentalchat.pojo.Symptom;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;

@Component
public class Neo4jDataUtils {


    public void getJsonData(List<Disease> diseases, List<Symptom> symptoms, List<PatientDescription> patientDescriptions) {
        String filePath = "C:\\Users\\11785\\IdeaProjects\\mentalchat\\src\\main\\resources\\static\\parsed_kg_info.json"; // 替换为你的JSON文件路径
        try (FileReader reader = new FileReader(filePath)) {
            JSONObject jsonObject = JSON.parseObject(reader);
            JSONArray diseaseList = jsonObject.getJSONArray("id2disease");
            JSONArray symptomList = jsonObject.getJSONArray("id2symp");
            JSONArray descList = jsonObject.getJSONArray("id2desc");
            JSONArray symp_id2disease_ids = jsonObject.getJSONArray("symp_id2disease_ids");
            JSONArray symp_id2desc_range = jsonObject.getJSONArray("symp_id2desc_range");
            HashMap<Long, Disease> diseaseHashMap = new HashMap<>();
            for (int i = 0; i < descList.size(); i++) {
                PatientDescription patientDescription = new PatientDescription();
                patientDescription.setId((long) i);
                patientDescription.setText(descList.getString(i));
                patientDescriptions.add(patientDescription);
            }
            for (int i = 0; i < symp_id2desc_range.size(); i++) {
                JSONArray jsonArray = symp_id2desc_range.getJSONArray(i);
                Symptom symptom = new Symptom();
                symptom.setId((long) i);
                symptom.setName(symptomList.getString(i));
                symptom.setDescriptions(new HashSet<>());
                for (int j = jsonArray.getInteger(0); j < jsonArray.getInteger(1); j++) {
                    PatientDescription patientDescription = new PatientDescription();
                    patientDescription.setId((long) j);
                    patientDescription.setText(descList.getString(j));
                    symptom.getDescriptions().add(patientDescription);
                }
                symptoms.add(symptom);
            }
            for (int i = 0; i < symp_id2disease_ids.size(); i++) {
                JSONArray disease_ids = symp_id2disease_ids.getJSONArray(i);
                for (int j = 0; j < disease_ids.size(); j++) {
                    if (diseaseHashMap.containsKey(disease_ids.getLong(j))) {
                        Disease disease = diseaseHashMap.get(disease_ids.getLong(j));
                        disease.getCauses().add(symptoms.get(i));
                    } else {
                        Disease disease = new Disease();
                        disease.setId(disease_ids.getLong(j));
                        disease.setName(diseaseList.getString(disease_ids.getInteger(j)));
                        HashSet<Symptom> set = new HashSet<>();
                        set.add(symptoms.get(i));
                        disease.setCauses(set);
                        diseaseHashMap.put(disease_ids.getLong(j), disease);
                    }
                }
            }
            diseases.addAll(new ArrayList<>(diseaseHashMap.values()));
        } catch (IOException ex) {
            throw new RuntimeException(ex);
        }
    }
}
