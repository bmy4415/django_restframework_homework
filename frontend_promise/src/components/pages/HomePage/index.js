import React from 'react';
import { Login, PromiseList, AddPromise, Logout } from "../../../containers";
import { connect } from "react-redux";

/**
 * if(userId) means login successed
 */

const mapStateToProps = (state) => {
	return {
		userId: state.promises.userId,
	};
};


const HomePage = ({ userId }) => {
	if(userId) {
		return (
			<div>
				<PromiseList/>
				<AddPromise/>
				<Logout/>
			</div>
		);
	}

	return (
		<Login/>
	);

};

export default connect(mapStateToProps)(HomePage);
