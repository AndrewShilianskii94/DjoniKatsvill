from unittest.mock import patch

from utils import add_comment, add_bookmark, delete_post, delete_comment, delete_bookmark


def test_add_comment():
    with patch('utils.save_json_file') as mock_save_json:
        # Input data
        comments = [{'pk': 1, 'text': 'Comment 1'}]
        new_comment = {'pk': 2, 'text': 'Comment 2'}
        # Expected data
        expected_comments = [{'pk': 1, 'text': 'Comment 1'}, {'pk': 2, 'text': 'Comment 2'}]
        # Call the function being tested
        add_comment(new_comment)
        # Check that the save_json_file function was called with the correct arguments
        mock_save_json.assert_called_once_with('C:/Users/Андрей/PycharmProjects/DjoniKatsvill/data/comments.json',
                                               expected_comments)


def test_add_bookmark():
    with patch('utils.save_json_file') as mock_save_json:
        # Input data
        bookmarks = [{'pk': 1, 'url': 'https://example.com'}]
        new_bookmark = {'pk': 2, 'url': 'https://example.org'}
        # Expected data
        expected_bookmarks = [{'pk': 1, 'url': 'https://example.com'}, {'pk': 2, 'url': 'https://example.org'}]
        # Call the function being tested
        add_bookmark(new_bookmark)
        # Check that the save_json_file function was called with the correct arguments
        mock_save_json.assert_called_once_with('C:/Users/Андрей/PycharmProjects/DjoniKatsvill/data/bookmarks.json',
                                               expected_bookmarks)


def test_delete_post():
    with patch('utils.save_json_file') as mock_save_json:
        # Input data
        posts = [{'pk': 1, 'title': 'Post 1'}, {'pk': 2, 'title': 'Post 2'}]
        post_id = 2
        # Expected data
        expected_posts = [{'pk': 1, 'title': 'Post 1'}]
        # Call the function being tested
        delete_post(post_id)
        # Check that the save_json_file function was called with the correct arguments
        mock_save_json.assert_called_once_with('C:/Users/Андрей/PycharmProjects/DjoniKatsvill/data/posts.json',
                                               expected_posts)


def test_delete_comment():
    with patch('utils.save_json_file') as mock_save_json:
        # Input data
        comments = [{'pk': 1, 'text': 'Comment 1'}, {'pk': 2, 'text': 'Comment 2'}]
        comment_id = 2
        # Expected data
        expected_comments = [{'pk': 1, 'text': 'Comment 1'}]
        # Call the function being tested
        delete_comment(comment_id)
        # Check that the save_json_file function was called with the correct arguments
        mock_save_json.assert_called_once_with('C:/Users/Андрей/PycharmProjects/DjoniKatsvill/data/comments.json',
                                               expected_comments)


def test_delete_bookmark():
    with patch('utils.save_json_file') as mock_save_json:
        # Input data
        bookmarks = [{'pk': 1, 'url': 'https://example.com'}, {'pk': 2, 'url': 'https://example.org'}]
        bookmark_id = 2
        # Expected data
        expected_bookmarks = [{'pk': 1, 'url': 'https://example.com'}]
        # Call the function being tested
        delete_bookmark(bookmark_id)
        # Check that the save_json_file function was called with the correct arguments
        mock_save_json.assert_called_once_with('C:/Users/Андрей/PycharmProjects/DjoniKatsvill/data/bookmarks.json',
                                               expected_bookmarks)
