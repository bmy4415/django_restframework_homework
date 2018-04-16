import React, { PropTypes } from 'react';
import Button from "../../atoms/Button";


const Login = ({ onClickTodo }) => {
	let username = null;
	let password = null;
	
	console.log("here is login component");


	const onSubmit = () => {
		if(username && password) {
			onClickTodo(username.value, password.value);
			username.value = "";
			password.value = "";
		}

	};

	return (
		<div>
			<h1>username</h1>
			<input ref={node => { username = node; }}/>
			<h1>password</h1>
			<input type="password" ref={node => { password = node; }}/>
			<Button type="submit" onClick={onSubmit}>LOGIN</Button>
		</div>
	);
}

Login.propTypes = {
  // reverse: PropTypes.bool,
  // children: PropTypes.node,
	onClickTodo: PropTypes.func.isRequired
};

export default Login;
