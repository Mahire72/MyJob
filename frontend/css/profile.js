body {
    font-family: Arial, sans-serif;
    background-color: #a79dbd;
    margin: 0;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 30px;
    background-color: #947b8d;
    color: white;
}

.navbar h1 {
    margin: 0;
    font-size: 20px;
}

.navbar button {
    background: white;
    color: #007bff;
    border: none;
    padding: 8px 15px;
    border-radius: 6px;
    cursor: pointer;
}

.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: calc(100vh - 60px);
}

form {
    background: pink;
    padding: 50px;
    border-radius: 10px;
    width: 300px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

input, select {
    padding: 10px;
    border: 1px solid #500909;
    border-radius: 6px;
}

button {
    padding: 10px;
    border: none;
    border-radius: 6px;
    background-color: #007bff;
    color: white;
    cursor: pointer;
}

button:hover {
    background-color: #6b0b0b;
}