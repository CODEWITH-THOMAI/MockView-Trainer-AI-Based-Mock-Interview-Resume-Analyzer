# 🚀 Supabase Setup Guide

## Overview
This guide will help you set up Supabase for the MockView Trainer application, replacing Firebase.

---

## Step 1: Create Supabase Project

1. Go to https://supabase.com
2. Click **"Start your project"**
3. Sign in with GitHub (recommended)
4. Click **"New Project"**
5. Fill in the project details:
   - **Name**: `MockView-Trainer` (or your preferred name)
   - **Database Password**: Generate a strong password and **SAVE IT** (you'll need this!)
   - **Region**: Choose the region closest to your users
   - **Pricing Plan**: Select **Free** tier to start
6. Click **"Create new project"**
7. Wait 2-3 minutes for your project to be provisioned

---

## Step 2: Get API Keys

1. In your Supabase project dashboard, navigate to **Settings** → **API**
2. Copy the following values (you'll need these for your `.env` files):
   - **Project URL**: `https://xxxxxxxxxxxxx.supabase.co`
   - **anon public key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (for frontend)
   - **service_role key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (for backend - **KEEP SECRET!**)

⚠️ **Important**: The service_role key has admin privileges. Never expose it in frontend code or commit it to version control!

---

## Step 3: Set Up Database Schema

1. In your Supabase dashboard, go to **SQL Editor**
2. Click **"New Query"**
3. Open the file `backend/database/schema.sql` from this repository
4. Copy the **entire contents** of the file
5. Paste it into the SQL Editor
6. Click **"Run"** (or press `Ctrl/Cmd + Enter`)
7. You should see: **"Success. No rows returned"**
8. Navigate to **Table Editor** to verify that 5 tables were created:
   - `users`
   - `interview_sessions`
   - `fluency_tests`
   - `resumes`
   - `chat_history`

---

## Step 4: Enable Email Authentication

1. Go to **Authentication** → **Providers**
2. **Email** should be enabled by default (confirm it's on)
3. Optionally customize email templates:
   - Navigate to **Authentication** → **Email Templates**
   - Customize confirmation emails, reset password emails, etc.
4. Configure URL settings:
   - Go to **Authentication** → **URL Configuration**
   - **Site URL**: `http://localhost:5173` (for development)
   - **Redirect URLs**: Add `http://localhost:5173/**`

For production:
- Update Site URL to your production frontend URL
- Add your production domain to Redirect URLs

---

## Step 5: Set Up Storage (Optional - for Resume Uploads)

1. Go to **Storage** in the Supabase dashboard
2. Click **"Create a new bucket"**
3. Configure the bucket:
   - **Name**: `resumes`
   - **Public**: Leave **unchecked** (private bucket)
   - **File size limit**: 16 MB (or as needed)
4. Click **"Create bucket"**
5. Set up storage policies:
   - Click on the `resumes` bucket → **Policies**
   - Click **"New Policy"** → **"For full customization"**
   - Add policy:
     ```sql
     -- Allow users to upload to their own folder
     CREATE POLICY "Users can upload own resumes"
     ON storage.objects FOR INSERT
     TO authenticated
     WITH CHECK (
       bucket_id = 'resumes' AND
       (storage.foldername(name))[1] = auth.uid()::text
     );

     -- Allow users to read their own resumes
     CREATE POLICY "Users can read own resumes"
     ON storage.objects FOR SELECT
     TO authenticated
     USING (
       bucket_id = 'resumes' AND
       (storage.foldername(name))[1] = auth.uid()::text
     );
     ```

---

## Step 6: Configure Environment Variables

### Backend Configuration
Create or update `backend/.env` file:

```bash
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production
PORT=5000

# Frontend URL for CORS
FRONTEND_URL=http://localhost:5173

# Supabase Configuration
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key-here
SUPABASE_ANON_KEY=your-anon-public-key-here

# File Upload Configuration
UPLOAD_FOLDER=uploads
```

⚠️ Replace the placeholder values with your actual Supabase credentials from Step 2.

### Frontend Configuration
Create or update `.env` file in the project root:

```bash
# Backend API
VITE_API_URL=http://localhost:5000/api

# Supabase Configuration
VITE_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-public-key-here
```

⚠️ Only use the **anon public key** in the frontend, never the service_role key!

---

## Step 7: Install Dependencies

### Backend
```bash
cd backend
pip install -r requirements.txt
```

### Frontend
```bash
npm install
```

---

## Step 8: Test the Connection

### Test Backend Connection
```bash
cd backend
python -c "from database.supabase_config import test_connection; test_connection()"
```

Expected output:
```
✓ Supabase connected successfully
```

If you see an error, check:
- Your environment variables are set correctly
- Your Supabase project is running
- The database schema was applied successfully

### Start the Application
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
npm run dev
```

---

## Step 9: Verify Everything Works

1. Open your browser to `http://localhost:5173`
2. Try to **sign up** with a new account
3. Check Supabase dashboard:
   - Go to **Authentication** → **Users** (you should see your new user)
   - Go to **Table Editor** → **users** (you should see the user profile)
4. Try **logging in** with the account you just created
5. Test other features (interview, fluency test, etc.)

---

## 🔒 Security Best Practices

### Row Level Security (RLS)
The provided schema enables RLS on all tables. This ensures:
- Users can only access their own data
- Database operations are automatically filtered by user ID
- Additional security layer beyond application logic

### Key Management
- ✅ **DO**: Store service_role key in backend `.env` file
- ✅ **DO**: Add `.env` to `.gitignore`
- ✅ **DO**: Use environment variables in production (not `.env` files)
- ❌ **DON'T**: Commit API keys to version control
- ❌ **DON'T**: Use service_role key in frontend code
- ❌ **DON'T**: Share credentials publicly

---

## 🐛 Troubleshooting

### "Database not available" error
- Check that `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` are set in `backend/.env`
- Verify the keys are correct (no extra spaces or quotes)
- Ensure your Supabase project is active

### "Invalid token" error
- Make sure you're using the correct anon key in frontend
- Check that the token is being sent in the Authorization header
- Try logging out and logging in again

### "User not found" after signup
- Check that the database schema was applied correctly
- Verify the `users` table exists in Table Editor
- Check the backend logs for errors during user creation

### RLS Policy Errors
- If you get permission errors, check that RLS policies are set up correctly
- You may need to temporarily disable RLS for debugging: `ALTER TABLE table_name DISABLE ROW LEVEL SECURITY;`
- Remember to re-enable RLS after debugging!

---

## 🎯 Next Steps

1. ✅ Set up custom email templates for better branding
2. ✅ Configure password requirements in Auth settings
3. ✅ Set up database backups (automatic in Supabase)
4. ✅ Monitor usage in Supabase dashboard
5. ✅ Review RLS policies for your specific use case
6. ✅ Set up staging/production environments

---

## 📚 Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Auth Documentation](https://supabase.com/docs/guides/auth)
- [Supabase Storage Documentation](https://supabase.com/docs/guides/storage)
- [Row Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)
- [Supabase Python Client](https://supabase.com/docs/reference/python/introduction)
- [Supabase JavaScript Client](https://supabase.com/docs/reference/javascript/introduction)

---

## 🆘 Need Help?

- Check [Supabase Community](https://github.com/supabase/supabase/discussions)
- Join [Supabase Discord](https://discord.supabase.com)
- Review [GitHub Issues](https://github.com/supabase/supabase/issues)

---

## ✅ Migration Complete!

You've successfully migrated from Firebase to Supabase! Enjoy the benefits of:
- ✅ PostgreSQL power and flexibility
- ✅ Better developer experience
- ✅ Real-time capabilities
- ✅ Row Level Security
- ✅ More generous free tier
- ✅ Open-source and self-hostable

Happy coding! 🎉
