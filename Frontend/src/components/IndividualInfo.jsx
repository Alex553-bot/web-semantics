import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const host = 'http://localhost:5000';

function IndividualInfo() {
  const { nameClass, individualName } = useParams();
  const [individual, setIndividual] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      await fetch(`${host}/searchClass?query=${nameClass.replace('ontology.owx.', '')}`)
        .then(response => response.json())
        .then(data => {
          console.log(data.find(d => d.name === individualName));
          setIndividual(data.find(d => d.name === individualName));
        })
        .catch(error => console.error(error));
    }

    fetchData();
  }, [nameClass]);

  return (
    <div>
      {individual && (
        <div>
          <h4>{individual.name}</h4>
          <a href={individual.iri}>{individual.iri}</a>
          <div>
            {individual.individual.map((k, i) => (
              <div key={i}>
                {k.properties.map((item, j) => {
                  const [k, v] = Object.entries(item)[0];

                  return (<p key={j}><strong>{k}: </strong> {v}</p>);
                })}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default IndividualInfo;
