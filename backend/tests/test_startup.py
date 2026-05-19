import pytest
from unittest.mock import MagicMock, patch
from datetime import UTC, datetime, timedelta
from jose import jwt
from app.modules.auth.token import create_access_token
from app.core.startup import run_startup_tasks, setup_test_users, auto_seed_data
from app.modules.auth.models import User
from fastapi import HTTPException

def test_create_access_token_dev_long_expiry():
    """Test that tokens in dev mode have a very long expiry."""
    mock_settings = MagicMock()
    mock_settings.is_dev = True
    mock_settings.secret_key = "test_secret"
    mock_settings.jwt_algorithm = "HS256"
    
    with patch("app.modules.auth.token.get_settings", return_value=mock_settings):
        token = create_access_token({"sub": "user@example.com"})
        payload = jwt.decode(token, "test_secret", algorithms=["HS256"])
        
        exp = payload["exp"]
        expected_min_exp = (datetime.now(UTC) + timedelta(days=365 * 99)).timestamp()
        assert exp > expected_min_exp

def test_create_access_token_prod_normal_expiry():
    """Test that tokens in prod mode have normal expiry."""
    mock_settings = MagicMock()
    mock_settings.is_dev = False
    mock_settings.access_token_expire_minutes = 60
    mock_settings.secret_key = "test_secret"
    mock_settings.jwt_algorithm = "HS256"
    
    with patch("app.modules.auth.token.get_settings", return_value=mock_settings):
        token = create_access_token({"sub": "user@example.com"})
        payload = jwt.decode(token, "test_secret", algorithms=["HS256"])
        
        exp = payload["exp"]
        # Should be roughly 60 minutes from now
        expected_exp = (datetime.now(UTC) + timedelta(minutes=60)).timestamp()
        assert abs(exp - expected_exp) < 10 # Allow 10s difference

def test_setup_test_users(db, test_settings):
    """Test that test users are created if they don't exist."""
    # Ensure user doesn't exist in the current transaction
    primary_dev_user = test_settings.dev_users[0]
    user = db.query(User).filter(User.email == primary_dev_user["email"]).first()
    if user:
        db.delete(user)
        db.flush()
    
    setup_test_users(db, test_settings.dev_users)
    
    user = db.query(User).filter(User.email == primary_dev_user["email"]).first()
    assert user is not None
    assert user.email == primary_dev_user["email"]

@patch("app.core.startup.seed_all")
def test_auto_seed_data_empty_db(mock_seed_all, db):
    """Test that seeding is called when DB is empty."""
    mock_seed_all.return_value = None
    auto_seed_data(db)
    mock_seed_all.assert_called_once()

@patch("app.core.startup.seed_all")
def test_auto_seed_data_already_seeded(mock_seed_all, db):
    """Test that seeding is skipped if DB already has data (simulated by HTTPException 405)."""
    mock_seed_all.side_effect = HTTPException(status_code=405, detail="Action is only allowed on empty database")
    
    # This should not raise an exception, just log and return
    auto_seed_data(db)
    mock_seed_all.assert_called_once()

def test_run_startup_tasks_dev_calls_subtasks(db):
    """Test that all dev startup tasks are triggered in dev mode."""
    mock_settings = MagicMock()
    mock_settings.is_dev = True
    mock_settings.is_demo = False
    mock_settings.dev_users = [{"email": "user@example.com", "password": "password"}]
    
    with patch("app.core.startup.setup_test_users") as mock_setup_users, \
         patch("app.core.startup.auto_seed_data") as mock_auto_seed:
        run_startup_tasks(db, mock_settings)
        mock_setup_users.assert_called_once_with(db, mock_settings.dev_users)
        mock_auto_seed.assert_called_once_with(db)
