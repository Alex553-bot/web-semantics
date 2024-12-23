import { Card } from 'react-bootstrap';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const host = 'http://localhost:5000';

function IndividualInfo() {
  const { locale, nameClass, individualIri } = useParams();
  const [individual, setIndividual] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      await fetch(`${host}/searchClass?query=${decodeURIComponent(nameClass).replace('ontology.owx.', '')}&lang=${locale}`)
        .then(response => response.json())
        .then(data => {
          setIndividual(data.find(d => d.iri === decodeURIComponent(individualIri)));
        })
        .catch(error => console.error(error));
    }

    fetchData();
  }, [nameClass]);

  return (
    <div className="d-flex justify-content-center">
      {individual && (
        <Card className="w-75">
          <Card.Body className="d-flex flex-column align-items-center">
            <Card.Title>{individual.name_individual}</Card.Title>
            <Card.Text>
              <a href={individual.iri} className="border p-2 d-block text-center">
                Sobre: {individual.name_individual}
              </a>
            </Card.Text>
            {individual.properties.map((obj, i) => {
              const [k, v] = Object.entries(obj)[0];

              if (typeof v !== 'object') {
                return (
                  <div key={i} className="d-flex flex-column align-items-center">
                    <strong>{k}: </strong>{v}
                  </div>
                );
              }
              return null;
            })}
          </Card.Body>
        </Card>
      )}
    </div>
  );
}

export default IndividualInfo;
