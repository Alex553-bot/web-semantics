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
    <div>
      {individual && (
        <div>
          <h4>{individual.name_individual}</h4>
          <a href={individual.iri}>{individual.iri}</a>

          {individual.properties.map((obj, i) => {
            const [k, v] = Object.entries(obj)[0];

            if (typeof v !== 'object') {
              return (<div key={i}><strong>{k}: </strong>{v}</div>);
            }
          })}
        </div>
      )}
    </div>
  );
}

export default IndividualInfo;
