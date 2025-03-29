import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col, Form, Button, Table } from 'react-bootstrap';
import { computeResults } from '../api/Results';
import MessageDisplay from '../components/MessageDisplay';



function Results(){

    const { connectionId } = useParams();

    const [inputText, setInputText] = useState('');
    const [showTable, setShowTable] = useState(false);
    const [data, setData] = useState([]);
    const [headers, setHeaders] = useState([]);
    const [messages, setMessages] = useState([]);

    
    /*
    const sampleData = [
        { "key_1": "aaaaa", "key_2": "vvvvvvv","key_4": "aaaaa","key_5": "aaaaa" },
        { "key_1": "bbbbb", "key_2": "wwwwwww","key_4": "aaaaa","key_5": "aaaaa" },
        { "key_1": "ccccc", "key_2": "xxxxxxx","key_4": "aaaaa" ,"key_5": "aaaaa"}
      ];

  */

      const handleInputChange = (e) => {
        setInputText(e.target.value);
      };

  const handleSubmit = async () => {

     await computeResults(connectionId, inputText,
      (data) => { 
        setData(data); 
        setMessages([{ type: 'success', text: 'Данные успешно загружены' }]);
      },
       (error) => console.log(error)
    )

    setShowTable(true);
  };


  useEffect(() => {
    if (data.length > 0) {
      setHeaders(Object.keys(data[0]));
    }
  }, [data]);

  return (
    <Container>
      <Row className="mt-5">
        <Col>
        <div className="d-flex align-items-stretch"
            style={{ borderRadius: '8px' , backgroundColor: 'white', marginTop:"10px" }}>
            <Form.Control
              as="textarea"
              rows={2}
              value={inputText}
              onChange={handleInputChange}
              placeholder="Введите данные здесь..."
              style={{ flex: 1, border: "0px", resize: "none" }}
            />
            <div className="d-flex justify-content-end">
            <Button
              variant="light"
              onClick={handleSubmit}
              style={{ backgroundColor: 'white', height: '100%' , border: '0px solid #ced4da' }}>
              Отправить
            </Button>
            </div>
        </div>
          </Col>
      </Row>
      {showTable && (
        <Row className="mt-5">
          <Col>
            <Table striped bordered hover>
              <thead>
                <tr>
                  {headers.map(key => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.map((row, index) => (
                  <tr key={index}>
                    {headers.map(header => (
                      <td key={header}>{row[header]}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </Table>
          </Col>
        </Row>
      )}
      <MessageDisplay messages={messages} />
    </Container>
  );
};

export default Results;