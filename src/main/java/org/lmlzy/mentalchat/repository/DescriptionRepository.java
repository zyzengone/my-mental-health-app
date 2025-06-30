package org.lmlzy.mentalchat.repository;

import org.lmlzy.mentalchat.pojo.PatientDescription;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DescriptionRepository extends Neo4jRepository<PatientDescription, Long> {
}
