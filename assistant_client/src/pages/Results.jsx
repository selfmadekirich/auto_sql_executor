import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';
import { computeResults, LoadMoreResults } from '../api/Results';
import { Notifications } from "react-push-notification";
import { successNotification, errorNotification } from '../utils';
import { fetchProfilesPartial } from '../api/Profiles';
import { InfiniteLoopTable } from '../components/InfiniteLoopTable';
import Loading from '../components/Loading';


function Results(){

    const { connectionId } = useParams();

    const [inputText, setInputText] = useState('');
    const [showTable, setShowTable] = useState(false);
    const [data, setData] = useState([]);
    const [headers, setHeaders] = useState([]);
    const [selectedOption, setSelectedOption] = useState('');
    const [options, setOptions] = useState([]);
    const [page, setPage] = useState(2)
    const [sqlQuery, setSqlQuery] = useState('')
    const [isLoading, setIsLoading] = useState(false);
    
    /*
    const sampleData = [
        { "key_1": "aaaaa", "key_2": "vvvvvvv","key_4": "aaaaa","key_5": "aaaaa" },
        { "key_1": "bbbbb", "key_2": "wwwwwww","key_4": "aaaaa","key_5": "aaaaa" },
        { "key_1": "ccccc", "key_2": "xxxxxxx","key_4": "aaaaa" ,"key_5": "aaaaa"}
      ];

  */

      useEffect(() => {
        fetchProfilesPartial(setOptions,
          (error) => {errorNotification(error.message)}
         )
         
      }, []);

      

      const handleSelectChange = (e) => {
        setSelectedOption(e.target.value);
      };


      const handleInputChange = (e) => {
        setInputText(e.target.value);
      };

  const handleSubmit = async () => {
    setIsLoading(true);
    setData([])
    setHeaders([])
    successNotification("" ,"Начинаем считать")
     console.log(selectedOption)
     await computeResults(connectionId, inputText, selectedOption,
      (data) => { 
        setData(data.result); 
        console.log(data.result);
        setSqlQuery(data.info.generated_sql);
        successNotification("","Успешно посчитали!")
        setShowTable(true);
        setIsLoading(false)
      },
       (error) => { errorNotification(error.message);}
    )
  };

  const fetchMoreData = async () => {
    await LoadMoreResults(connectionId, sqlQuery, page, (loaded) => {
      setPage(page + 1);
      setData(data.concat(loaded.results))
    }, 
    (error) => { errorNotification(error.message);}
    )
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
            <Form.Select
                value={selectedOption}
                onChange={handleSelectChange}
                style={{ marginRight: '10px' }}
              >
                <option value="">Выберете ИИ профиль</option>
                {options.map(option => (
                  <option key={option.Profile_id} value={option.Profile_id}>{option.profile_name}</option>
                ))}
              </Form.Select>
            </div>
        </div>
          </Col>
      </Row>
      { isLoading ? ( <Loading/>) : (
      showTable && (
        <Row className="mt-5">
          <Col>
          <InfiniteLoopTable headers={headers} data={data} update={fetchMoreData}></InfiniteLoopTable>
          </Col>
        </Row>
      ))}
      
      <Notifications position='bottom-left'/>
    </Container>
  );
};

export default Results;