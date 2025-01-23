// IncomeReview.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const IncomeReview = () => {
    const [income, setIncome] = useState([]);
    const [amount, setAmount] = useState('');
    const [description, setDescription] = useState('');
    const [date, setDate] = useState('');

    useEffect(() => {
        axios.get('/api/income/', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        })
        .then(response => setIncome(response.data))
        .catch(error => console.error('Error fetching income:', error));
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('/api/income/', {
            amount,
            description,
            date
        }, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        })
        .then(response => {
            setIncome([...income, response.data]);
            setAmount('');
            setDescription('');
            setDate('');
        })
        .catch(error => console.error('Error adding income:', error));
    };

    return (
        <div>
            <h2>Income Review</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="Amount"
                    required
                />
                <input
                    type="text"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Description"
                    required
                />
                <input
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                    required
                />
                <button type="submit">Add Income</button>
            </form>
            <ul>
                {income.map(item => (
                    <li key={item.id}>
                        {item.amount} - {item.description} - {item.date}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default IncomeReview;
