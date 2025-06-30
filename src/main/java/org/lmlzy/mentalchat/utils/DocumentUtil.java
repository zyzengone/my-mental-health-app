package org.lmlzy.mentalchat.utils;

import org.springframework.ai.document.Document;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class DocumentUtil {
    @jakarta.annotation.Resource
    private ResourceLoader resourceLoader;
    public static List<Document> readDocumentsFromFile(Resource filePath) throws IOException {
        String txt = readFileToString(filePath);
        Document[] documentsArray = new Document[1];
        Document document = new Document(txt);
        documentsArray[0] = document;
        return List.of(documentsArray);
    }
    public static String readJsonFileToString(Resource filePath) throws IOException {
        StringBuilder result = new StringBuilder();
        try (InputStream inputStream = filePath.getInputStream();
             InputStreamReader inputStreamReader = new InputStreamReader(inputStream, StandardCharsets.UTF_8);
             BufferedReader bufferedReader = new BufferedReader(inputStreamReader)) {

            String line;
            while ((line = bufferedReader.readLine()) != null) {
                result.append(line).append(System.lineSeparator());
            }
        }
        return result.toString();
    }

    public static String readFileToString(Resource resource) throws IOException {
        StringBuilder result = new StringBuilder();

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(resource.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) {
                result.append(line).append("\n");
            }
        }

        return result.toString().trim();
    }
}
