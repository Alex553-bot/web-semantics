import React from 'react';
import { Card } from 'react-bootstrap';

function Result(props) {
  const { nameClass, arrayClass } = props;

  return (
    <div>
      <Card>
        <Card.Body>
          <Card.Header><h5>{ nameClass }</h5></Card.Header>
          {arrayClass.map(a => (
            <React.Fragment key={a.iri}>
              <Card.Subtitle className='mt-1'><a href={a.iri}>{a.iri}</a></Card.Subtitle>
              <Card.Subtitle className='mt-1'>{a.name}</Card.Subtitle>
            </React.Fragment>
          ))}
        </Card.Body>
      </Card>
    </div>
  );
}

export default Result;
