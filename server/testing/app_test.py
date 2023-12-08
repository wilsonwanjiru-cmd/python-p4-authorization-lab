from app import app
from models import Article, User

class TestApp:
    '''Flask API in app.py'''

    def test_can_only_access_member_only_article_index_while_logged_in(self):
        '''allows logged in users to access member-only article index at /members_only_articles.'''
        with app.test_client() as client:

            client.get('/clear')

            user = User.query.first()
            client.post('/login', json={
                'username': user.username
            })

            response = client.get('/members_only_articles')
            assert response.status_code == 200

            client.delete('/logout')

            response = client.get('/members_only_articles')
            assert response.status_code == 401

    def test_member_only_articles_shows_member_only_articles(self):
        '''only shows member-only articles at /members_only_articles.'''
        with app.test_client() as client:

            client.get('/clear')

            user = User.query.first()
            client.post('/login', json={
                'username': user.username
            })

            response_json = client.get('/members_only_articles').get_json()
            for article in response_json:
                assert article['is_member_only'] == True

    def test_can_only_access_full_member_only_article_while_logged_in(self):
        '''allows logged in users to access full member-only articles at /members_only_articles/<int:id>.'''
        with app.test_client() as client:

            client.get('/clear')

            user = User.query.first()
            client.post('/login', json={
                'username': user.username
            })

            # Get the ID of a member-only article
            member_only_article = Article.query.filter_by(is_member_only=True).first()
            article_id = member_only_article.id if member_only_article else 1  # Provide a fallback ID

            response = client.get(f'/members_only_articles/{article_id}')
            assert response.status_code == 200

            client.delete('/logout')

            response = client.get(f'/members_only_articles/{article_id}')
            assert response.status_code == 401
