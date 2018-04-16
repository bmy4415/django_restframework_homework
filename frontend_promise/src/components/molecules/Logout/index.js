import React, { PropTypes } from 'react';
import Button from "../../atoms/Button";


const Logout = ({ onClickTodo }) => {

	const onSubmit = () => {
		onClickTodo();
	};

	return (
		<Button type="submit" onClick={onSubmit}>LOGOUT</Button>
	);
}

Logout.propTypes = {
  // reverse: PropTypes.bool,
  // children: PropTypes.node,
	onClickTodo: PropTypes.func.isRequired
};

export default Logout;
