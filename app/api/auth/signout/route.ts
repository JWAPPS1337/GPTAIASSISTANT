import { NextResponse } from 'next/server';
import { signOut } from '@/lib/auth/local-auth';

export async function POST() {
  try {
    signOut();
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Sign out error:', error);
    return NextResponse.json(
      { error: 'An error occurred during sign out' },
      { status: 500 }
    );
  }
} 