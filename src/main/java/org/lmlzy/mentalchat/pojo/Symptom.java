package org.lmlzy.mentalchat.pojo;

import lombok.Data;
import org.springframework.data.neo4j.core.schema.GeneratedValue;
import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Relationship;

import java.util.Set;

@Node("Symptom")
@Data
public class Symptom {
    @Id
    private Long id;
    private String name;
    @Relationship(type = "HAS_DESCRIPTION", direction = Relationship.Direction.OUTGOING)
    private Set<PatientDescription> descriptions;
}
