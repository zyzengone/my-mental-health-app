package org.lmlzy.mentalchat.repository;

import org.lmlzy.mentalchat.pojo.Symptom;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SymptomRepository extends Neo4jRepository<Symptom, Long> {
}
