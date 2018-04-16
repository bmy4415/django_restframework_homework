import { connect } from "react-redux";
import PromiseList from "../components/molecules/PromiseList";
// import { tryLogin } from "../store/promises/actions";


const mapStateToProps = (state) => {
	return {
		// statefunction: state,
		response: state.promises.response,
		username: state.promises.username,
		userId: state.promises.userId
	};
};

const mapDispatchToProps = (dispatch) => {
	return {
		// onClickTodo: (username, password) => {
		//     dispatch(tryLogin(username, password));
		// }
	};
};

export default connect(mapStateToProps, mapDispatchToProps)(PromiseList);
