import { useState } from 'react';
import { Button, Col, Form, InputGroup, Row } from 'react-bootstrap';
import Result from './Result';
import messages_es from '../translations/es.json';
import messages_en from '../translations/en.json';
import messages_fr from '../translations/fr.json';
import messages_pt from '../translations/pt.json';
import { FormattedMessage, IntlProvider } from 'react-intl';
import './Search.css';

const messages = {
  es: messages_es,
  en: messages_en,
  fr: messages_fr,
  pt: messages_pt,
};
const translations = ['es', 'en', 'fr', 'pt'];
const host = 'http://localhost:5000';

function Search() {
  const [locale, setLocale] = useState('es');
  const [query, setQuery] = useState(null);
  const [result, setResult] = useState(null);
  const [isSearchClicked, setIsSearchClicked] = useState(false);
  
  const handleSubmit = async (e) => {
    e.preventDefault();

    await fetch(`${host}/search?query=${query}&lang=${locale}`)
      .then(response => response.json())
      .then(data => {
        setIsSearchClicked(true);
        setResult(data);
      })
      .catch(error => console.error(error));
  };

  const handleChangeTranslation = (e) => {
    e.preventDefault();
    setLocale(e.target.value);
    setResult(null); 
    setIsSearchClicked(false);
  };

  return (
    <div className='container'>
      <IntlProvider locale={locale} messages={messages[locale]}>
        <Row
          className={`align-items-center mx-auto transition-container ${
            isSearchClicked ? 'search-moved' : ''
          }`}
        >
          <Col xs={9} lassName='d-flex justify-content-center'>
            <Form onSubmit={handleSubmit} className='search-form' width="width: 100%">
              <div className='mt-3 mb-2'>
                <InputGroup size='lg'>
                  <Form.Control
                    placeholder={messages[locale]['app.placeholder']}
                    onChange={(e) => setQuery(e.target.value)}
                  />
                  <Button variant='secondary' id='search-button' type='submit'>
                    <FormattedMessage id='app.search-button' />
                  </Button>
                </InputGroup>
              </div>
            </Form>
          </Col>

          <Col xs={3} className="d-flex justify-content-center">
            <Form.Select onChange={handleChangeTranslation}>
              {translations.map(t => (
                <option key={t} value={t}>
                  <FormattedMessage id={t} />
                </option>
              ))}
            </Form.Select>
          </Col>
        </Row>

        <div className={`mx-auto results-container ${isSearchClicked ? 'show-results' : ''}`}>
          {result && Object.keys(result).map(k => (
            <div className='m-3' key={k}>
              <Result locale={locale} nameClass={k} arrayClass={result[k]} />
            </div>
          ))}
        </div>
      </IntlProvider>
    </div>
  );
}

export default Search;
