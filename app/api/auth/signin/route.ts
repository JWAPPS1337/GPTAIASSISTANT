import { NextRequest, NextResponse } from 'next/server';
import { signIn } from '@/lib/auth/local-auth';

export async function POST(request: NextRequest) {
  try {
    const { email, password } = await request.json();
    
    if (!email || !password) {
      return NextResponse.json(
        { error: 'Email and password are required' },
        { status: 400 }
      );
    }
    
    const session = signIn(email, password);
    
    if (!session) {
      return NextResponse.json(
        { error: 'Invalid credentials' },
        { status: 401 }
      );
    }
    
    return NextResponse.json({ session });
  } catch (error) {
    console.error('Sign in error:', error);
    return NextResponse.json(
      { error: 'An error occurred during authentication' },
      { status: 500 }
    );
  }
} 