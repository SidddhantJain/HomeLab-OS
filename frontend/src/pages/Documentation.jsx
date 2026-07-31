import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';
import { DocumentationSDK } from '../sdk';
import { BookOpen, Search, FileText, CornerDownRight, RefreshCw } from 'lucide-react';

const docSDK = new DocumentationSDK(apiClient);

const DocumentationPage = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [selectedDocPath, setSelectedDocPath] = useState('');
  const [docContent, setDocContent] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query) return;
    setLoading(true);
    try {
      const data = await docSDK.searchDocs(query);
      setResults(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const loadDocument = async (path) => {
    setLoading(true);
    try {
      setSelectedDocPath(path);
      const data = await docSDK.renderMarkdown(path);
      setDocContent(data.content);
    } catch (e) {
      setDocContent('Error loading documentation file contents.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Documentation Index</h1>
          <p className="text-slate-400 text-xs mt-1">Search or render public layouts and local codebase design manuals.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Search Sidebar */}
        <div className="glass-card border border-slate-800 p-5 rounded-2xl bg-gradient-to-br from-slate-900/40 to-slate-950/20 h-fit space-y-4">
          <form onSubmit={handleSearch} className="space-y-2">
            <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400">Search Workspace</label>
            <div className="relative">
              <input
                type="text"
                placeholder="Search wiki..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-950/40 border border-slate-800 text-slate-200 text-xs font-semibold outline-none focus:border-indigo-500 transition-all"
              />
              <Search className="absolute left-3 top-2.5 w-3.5 h-3.5 text-slate-500" />
            </div>
            <button
              type="submit"
              className="w-full py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs transition-all border border-slate-700"
            >
              Search
            </button>
          </form>

          {/* Preset guides */}
          <div className="space-y-2 pt-2">
            <span className="block text-[10px] font-bold uppercase tracking-wider text-slate-400">Quick Links</span>
            <div className="space-y-1 text-xs">
              <button
                onClick={() => loadDocument('Documentation/Public/Storage_Service_Architecture.md')}
                className="w-full text-left p-2 rounded-lg hover:bg-slate-900/40 text-slate-400 hover:text-white transition-all flex items-center gap-1.5"
              >
                <FileText className="w-3.5 h-3.5 shrink-0" />
                Storage Service Architecture
              </button>
              <button
                onClick={() => loadDocument('Documentation/Public/Vault_Service_Architecture.md')}
                className="w-full text-left p-2 rounded-lg hover:bg-slate-900/40 text-slate-400 hover:text-white transition-all flex items-center gap-1.5"
              >
                <FileText className="w-3.5 h-3.5 shrink-0" />
                Vault Service Architecture
              </button>
            </div>
          </div>
        </div>

        {/* Display / Search Results */}
        <div className="lg:col-span-3 space-y-4">
          {loading ? (
            <div className="flex justify-center py-12">
              <RefreshCw className="w-6 h-6 animate-spin text-indigo-500" />
            </div>
          ) : docContent ? (
            <div className="glass-card border border-slate-800 p-6 rounded-3xl bg-gradient-to-br from-slate-900/20 to-slate-950/10 space-y-4">
              <div className="flex justify-between items-center pb-3 border-b border-slate-800">
                <span className="text-[10px] font-mono text-slate-500">{selectedDocPath}</span>
                <button
                  onClick={() => setDocContent('')}
                  className="px-2.5 py-1 rounded-lg bg-slate-850 hover:bg-slate-800 text-[10px] text-slate-400 hover:text-white transition-all"
                >
                  Clear File View
                </button>
              </div>
              <pre className="text-xs text-slate-300 font-mono whitespace-pre-wrap leading-relaxed overflow-x-auto">
                {docContent}
              </pre>
            </div>
          ) : results.length > 0 ? (
            <div className="space-y-3">
              <h2 className="text-xs font-bold text-slate-400">Search results for query: "{query}"</h2>
              {results.map((r, idx) => (
                <div
                  key={idx}
                  onClick={() => loadDocument(r.path)}
                  className="glass-card border border-slate-850 p-4 rounded-xl hover:border-indigo-500/40 bg-slate-900/10 cursor-pointer hover:bg-slate-900/25 transition-all space-y-1"
                >
                  <h3 className="text-xs font-bold text-white flex items-center gap-1.5">
                    <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
                    {r.title}
                  </h3>
                  <p className="text-[10px] text-slate-500 font-mono flex items-center gap-1">
                    <CornerDownRight className="w-3 h-3 text-slate-700" />
                    {r.path}
                  </p>
                  <p className="text-xs text-slate-400 line-clamp-2 pt-1">{r.snippet}</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="glass-card border border-slate-800 p-8 rounded-2xl text-center text-slate-500">
              <BookOpen className="w-8 h-8 mx-auto text-slate-700 mb-2" />
              <p className="text-xs font-semibold">Select a quick link or search to begin.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DocumentationPage;
