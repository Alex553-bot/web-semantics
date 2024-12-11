import { useState } from 'react';
import { Button, Col, Form, InputGroup, Row } from 'react-bootstrap';
import Result from './Result';
import messages_es from '../translations/es.json';
import messages_en from '../translations/en.json';
import { FormattedMessage, IntlProvider } from 'react-intl';

const messages = {
  es: messages_es,
  en: messages_en,
}

const translations = ['es', 'en'];

function Search() {
  const [locale, setLocale] = useState('es');
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

  const handleChangeTranslation = (e) => {
    e.preventDefault();
    setLocale(e.target.value);
  }

  return (
    <div>
      <IntlProvider locale={locale} messages={messages[locale]}>
        <Row className='align-items-center'>
          <Col xs={9}>
            <Form onSubmit={handleSubmit}>
              <div className='mt-3 mb-2 mx-auto' style={{ width: '70%' }}>
                <InputGroup size='lg'>
                  <Form.Control
                    placeholder={messages[locale]['app.placeholder']}
                    onChange={(e) => setQuery(e.target.value) }
                  />
                  <Button
                    variant='outline-secondary'
                    id='search-button'
                    type='submit'
                  >
                    <FormattedMessage id='app.search-button' />
                  </Button>
                </InputGroup>
              </div>
            </Form>
          </Col>

          <Col xs={2}>
            <Form.Select onChange={handleChangeTranslation}>
              {translations.map(t => (
                <option value={t}>
                  <FormattedMessage id={t} />
                </option>
              ))}
            </Form.Select>
          </Col>
        </Row>

        <div className='mx-auto' style={{ width: '80%' }}>
          {result && Object.keys(result).map(k => (
            <div className='m-3'>
              <Result nameClass={k} arrayClass={result[k]} />
            </div>
          ))}
        </div>
      </IntlProvider>
    </div>
  );
}

export default Search;
