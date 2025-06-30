package org.lmlzy.mentalchat.component;

import org.lmlzy.mentalchat.utils.DocumentUtil;
import org.springframework.ai.document.Document;
import org.springframework.ai.ollama.OllamaEmbeddingModel;
import org.springframework.ai.ollama.api.OllamaApi;
import org.springframework.ai.vectorstore.SimpleVectorStore;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.Resource;


import java.io.IOException;
import java.util.List;

/**
 * @author thaivc
 * @since 2024
 */
@Configuration
public class VectorConfig {

    @Value("classpath:node.json")
    private Resource jsonFilePath;
    @Value("classpath:node.txt")
    private Resource txtFilePath;

    @Bean
    VectorStore vectorStore(OllamaEmbeddingModel embeddingModel) throws IOException {
        VectorStore simpleVectorStore = SimpleVectorStore.builder(embeddingModel).build();
        loadDocuments(simpleVectorStore);
        return simpleVectorStore;
    }
    private void loadDocuments(VectorStore vectorStore) throws IOException {
        List<Document> documents = DocumentUtil.readDocumentsFromFile(txtFilePath);
        vectorStore.add(documents);
    }
}
