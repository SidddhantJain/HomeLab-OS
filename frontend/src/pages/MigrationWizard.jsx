import React, { useState } from 'react';

export default function MigrationWizardPage() {
  const [step, setStep] = useState(1);

  return (
    <div style={{ padding: '24px', color: '#fff', fontFamily: 'sans-serif' }}>
      <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>Server Migration Assistant</h1>
      <p style={{ color: '#aaa', marginBottom: '24px' }}>Zero-Downtime Server Configuration & Database Transfer</p>

      <div style={{ background: 'rgba(255,255,255,0.05)', padding: '24px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)', maxWidth: '600px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '24px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '12px' }}>
          <span style={{ color: step === 1 ? '#00d2ff' : '#888', fontWeight: 'bold' }}>1. Export Source</span>
          <span style={{ color: step === 2 ? '#00d2ff' : '#888', fontWeight: 'bold' }}>2. Transfer State</span>
          <span style={{ color: step === 3 ? '#00d2ff' : '#888', fontWeight: 'bold' }}>3. Verify & Switch</span>
        </div>

        {step === 1 && (
          <div>
            <p style={{ color: '#ccc', marginBottom: '16px' }}>Export system configuration, database tables, and user preferences into a signed migration bundle.</p>
            <button onClick={() => setStep(2)} style={{ padding: '10px 20px', background: '#00d2ff', border: 'none', borderRadius: '4px', color: '#000', fontWeight: 'bold', cursor: 'pointer' }}>
              Begin Export →
            </button>
          </div>
        )}

        {step === 2 && (
          <div>
            <p style={{ color: '#ccc', marginBottom: '16px' }}>Transferring migration package to target HomeLab server (192.168.1.150)...</p>
            <div style={{ height: '8px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden', marginBottom: '16px' }}>
              <div style={{ height: '100%', width: '65%', background: '#00ff88' }} />
            </div>
            <button onClick={() => setStep(3)} style={{ padding: '10px 20px', background: '#00ff88', border: 'none', borderRadius: '4px', color: '#000', fontWeight: 'bold', cursor: 'pointer' }}>
              Complete Transfer →
            </button>
          </div>
        )}

        {step === 3 && (
          <div>
            <p style={{ color: '#00ff88', fontWeight: 'bold', marginBottom: '16px' }}>Migration Verification Complete! Target server operational.</p>
            <button onClick={() => setStep(1)} style={{ padding: '10px 20px', background: 'rgba(255,255,255,0.2)', border: 'none', borderRadius: '4px', color: '#fff', fontWeight: 'bold', cursor: 'pointer' }}>
              Finish Migration
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
