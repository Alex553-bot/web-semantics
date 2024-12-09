import { useState } from 'react';
import { Button, Form, InputGroup } from 'react-bootstrap';
import Result from './Result';

function Search() {
  const [query, setQuery] = useState(null);
  const [result, setResult] = useState(null);
  
  const handleSubmit = async (e) => {
    e.preventDefault();

    await fetch(`search?query=${query}`)
      .then(response => response.json())
      .then(data => {
        setResult(data);
      })
      .catch(error => console.error(error));
  }

  return (
    <div>
      <Form onSubmit={handleSubmit}>
        <div className='mt-3 mb-2 mx-auto' style={{ width: '50%' }}>
          <InputGroup size='lg'>
            <Form.Control
              placeholder='Escriba su búsqueda'
              onChange={(e) => setQuery(e.target.value) }
            />
            <Button
              variant='outline-secondary'
              id='search-button'
              type='submit'
            >
              Buscar
            </Button>
          </InputGroup>
        </div>
      </Form>

      <div className='mx-auto' style={{ width: '80%' }}>
        {result && Object.keys(result).map(k => (
          <div className='m-3'>
            <Result nameClass={k} arrayClass={result[k]} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default Search;
