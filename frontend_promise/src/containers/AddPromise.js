import { connect } from "react-redux";
import AddPromise from "../components/molecules/AddPromise";
import { addPromiseToServer } from "../store/promises/actions";


const mapStateToProps = (state) => {
	return {
		users: state.promises.users,
		userToken: state.promises.userToken,
	};
};

const mapDispatchToProps = (dispatch) => {
	return {
		onClickTodo: (sinceWhen, tilWhen, user2Username, users, userToken) => {
		    dispatch(addPromiseToServer(sinceWhen, tilWhen, user2Username, users, userToken));
		}
	};
};

export default connect(mapStateToProps, mapDispatchToProps)(AddPromise);
