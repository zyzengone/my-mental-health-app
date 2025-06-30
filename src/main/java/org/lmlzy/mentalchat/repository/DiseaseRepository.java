package org.lmlzy.mentalchat.repository;

import com.alibaba.fastjson2.JSONObject;
import org.lmlzy.mentalchat.pojo.Disease;
import org.neo4j.driver.types.Path;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DiseaseRepository extends Neo4jRepository<Disease, Long> {

    @Query("MATCH p=()-[r:CAUSES]->() RETURN p LIMIT 1000")
    List<Path> findCausesPaths();
}
