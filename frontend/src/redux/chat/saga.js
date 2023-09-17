import { 
  call, 
  put, 
  takeEvery,
  delay,
} from 'redux-saga/effects';
import apiAuthorizedClient from '../../helpers/apiAuthorizedClient';
import {
  FETCH_CHATS,
  ADD_CHAT,
  DELETE_CHAT,
  FETCH_MESSAGES,
  DELETE_MESSAGE,
} from './constants';
import {
  fetchChatsInitState,
  fetchChatsSuccess,
  fetchChatsFailed,

  addChatInitState,
  addChatSuccess,
  addChatFailed,

  deleteChatInitState,
  deleteChatSuccess,
  deleteChatFailed,

  fetchMessagesInitState,
  fetchMessagesSuccess,
  fetchMessagesFailed,

  deleteMessageInitState,
  deleteMessageSuccess,
  deleteMessageFailed,

  startWsConnection,
} from './actions';

const api = apiAuthorizedClient;

function* fetchChatsSaga() {
  try {
    const chats = yield call(api.get, '/chats/');
    yield put(fetchChatsSuccess(chats));
    yield delay(5000);
    yield put(fetchChatsInitState());
  } catch (errors) {
    yield put(fetchChatsFailed(errors));
  }
}

function* addChatSaga(action) {
  const data = action.payload;
  try {
      const chat = yield call(api.post, '/chats/', {
          "owner_id": data.user_id,
          "name": data.name,
          "addressee_id": 100
      });
      yield put(addChatSuccess(chat));
yield put(startWsConnection(chat.id));      
  } catch (errors) {
    yield put(addChatFailed(errors));
    yield delay(10000);
    yield put(addChatInitState());
  }
}

function* deleteChatSaga(action) {
  console.log("chat saga deleteChat action ", action);
  try {
    yield call(api.delete, `/chats/${action.payload}/`);
    yield put(deleteChatSuccess(action.payload));
    yield delay(5000);
    yield put(deleteChatInitState());
  } catch (errors) {
    yield put(deleteChatFailed(errors));
    yield delay(10000);
    yield put(deleteChatInitState());
  }
}

function* fetchMessagesSaga(action) {
  try {
    const messages = yield api.get(`/messages/?chat_id=${action.payload}`)
    yield put(fetchMessagesSuccess(messages));
yield put(startWsConnection(action.payload));
    yield delay(5000);
    yield put(fetchMessagesInitState());
  } catch (errors) {
    yield put(fetchMessagesFailed(errors));
  }
}

function* deleteMessageSaga(action) {
  try {
    yield call(api.delete, `/messages/${action.payload}/`);
    yield put(deleteMessageSuccess(action.payload));
    yield delay(5000);
    yield put(deleteMessageInitState());
  } catch (errors) {
    yield put(deleteMessageFailed(errors));
    yield delay(10000);
    yield put(deleteMessageInitState());
  }
}


export default function* chatSaga() {
  yield takeEvery(FETCH_CHATS, fetchChatsSaga);
  yield takeEvery(ADD_CHAT, addChatSaga);
  yield takeEvery(DELETE_CHAT, deleteChatSaga);
  yield takeEvery(FETCH_MESSAGES, fetchMessagesSaga);
  yield takeEvery(DELETE_MESSAGE, deleteMessageSaga);
}