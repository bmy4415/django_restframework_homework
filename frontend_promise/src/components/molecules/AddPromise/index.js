import React, { PropTypes } from 'react'
import Button from "../../atoms/Button";


class AddPromise extends React.Component {
	constructor(props) {
		super(props);
		this.sinceWhen = null;
		this.tilWhen = null;
		this.user2Username = null;
		this.onSubmit = this.onSubmit.bind(this);
	}

	onSubmit() {
		if(this.sinceWhen && this.tilWhen && this.user2Username) {
			this.props.onClickTodo(this.sinceWhen.value, this.tilWhen.value, this.user2Username.value, this.props.users, this.props.userToken);
			this.sinceWhen.value = "";
			this.tilWhen.value = "";
			this.user2Username.value = "";
		}
	}
	render() {
		return (
			<div>	
			<h1>You can add promise below</h1>
			<h5>sinceWhen</h5>
			<input ref={node => {this.sinceWhen = node}} />
			<h5>tilWhen</h5>
			<input ref={node => {this.tilWhen = node}} />
			<h5>user2 username</h5>
			<input ref={node => {this.user2Username = node}} />
			<Button type="submit" onClick={this.onSubmit}>ADD PROMISE</Button>
			</div>
		);
	}
}

AddPromise.propTypes = {
		reverse: PropTypes.bool,
		children: PropTypes.node,
}

export default AddPromise
