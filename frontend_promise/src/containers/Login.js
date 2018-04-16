import { connect } from "react-redux";
import Login from "../components/molecules/Login";
import { tryLogin } from "../store/promises/actions";


const mapStateToProps = (state) => {
	return {
		statefunction: state
	};
};

const mapDispatchToProps = (dispatch) => {
	return {
		onClickTodo: (username, password) => {
			dispatch(tryLogin(username, password));
		}
	};
};

export default connect(mapStateToProps, mapDispatchToProps)(Login);
