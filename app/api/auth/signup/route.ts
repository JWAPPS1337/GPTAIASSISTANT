import { NextRequest, NextResponse } from 'next/server';
import { createUser } from '@/lib/auth/local-auth';

export async function POST(request: NextRequest) {
  try {
    const { email, password, name } = await request.json();
    
    if (!email || !password) {
      return NextResponse.json(
        { error: 'Email and password are required' },
        { status: 400 }
      );
    }
    
    try {
      const user = createUser(email, password, name || email.split('@')[0]);
      return NextResponse.json({ user });
    } catch (err: any) {
      return NextResponse.json(
        { error: err.message },
        { status: 400 }
      );
    }
  } catch (error) {
    console.error('Sign up error:', error);
    return NextResponse.json(
      { error: 'An error occurred during registration' },
      { status: 500 }
    );
  }
} 