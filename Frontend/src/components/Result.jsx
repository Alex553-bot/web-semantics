import React from 'react';
import { Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';

function Result(props) {
  const { locale, nameClass, arrayClass } = props;

  return (
    <div>
      <Card>
        <Card.Body>
          <Card.Header><h5>{ nameClass }</h5></Card.Header>
          {arrayClass.map((a, i) => (
            <React.Fragment key={i}>
              { nameClass === 'DOID.dbpedia.Disease' ? 
                (
                  <Link target='_blank' to={a.iri}>
                    <Card.Subtitle className='m-2'>{a.name}</Card.Subtitle>
                  </Link>
                ) : (
                  <Link target='_blank' to={`${locale}/class/${encodeURIComponent(nameClass)}/individual/${encodeURIComponent(a.sample_name)}`}>
                    <Card.Subtitle className='m-2'>{a.name}</Card.Subtitle>
                  </Link>
                )
              }
            </React.Fragment>
          ))}
        </Card.Body>
      </Card>
    </div>
  );
}

export default Result;
